int main(){
    int x, y, z;

    // pre-conditions
    x = 0;
    y = 10;
    z = 0;

    // loop body
    while(unknown()){
        if(x == y){
            z = 0;
        }else{
            z = z + 1;
        } 
        x = (x + 1) % 10;
        y = (y - 1) % 10;
    }

    // post-condition
    assert(z <= 5);
    
}