int main(){
    int x, y, z;

    // pre-conditions
    assume((x == 0) || (x == 1));
    assume((y == 0) || (y == 1));
    z = 0;

    // loop body
    while(unknown()){
        if(((x % 2) == (y % 2))){
            z = z + 1;
        } 
        x = x + 2;
        y = y + 3;
    }

    // post-condition
    if(x > 400){
        assert(z >= 100);
    }
    
}