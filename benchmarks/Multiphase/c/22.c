int main(){
    int x, y, z;

    // pre-conditions
    x = 0;
    y = 767976;
    z = 0;

    // loop body
    while(unknown()){
        if((x - y) % 3 == 1){
            z = z + 3;
        }
        x = x + 1;
        y = y - 1;      
    }

    // post-condition
    if(x >= 280275){
        assert(z >= 280275);
    }
    
}